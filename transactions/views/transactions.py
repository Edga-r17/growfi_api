import os
import requests
import openai
from dotenv import load_dotenv
from django.db.models import Sum
from django.utils.timezone import now
from datetime import timedelta
from rest_framework.response import Response
from rest_framework.views import APIView
from transactions.models.transactions import Transaction
from transactions.serializers.transactions import TransactionSerializer
from _base.views import RequireUserTokenMixin


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise ValueError("Falta la clave API de OpenAI. Asegúrate de definir OPENAI_API_KEY en el archivo .env")

class TransactionCreateView(APIView, RequireUserTokenMixin):
    def post(self, request):
        lambda_url = "https://46vgroiqfk.execute-api.us-east-2.amazonaws.com/dev/"  

        try:
            # Enviar los datos a AWS Lambda
            response = requests.post(lambda_url, json=request.data)
            response_data = response.json()
        except requests.exceptions.RequestException as e:
            return Response({"error": "Error al conectar con AWS Lambda", "details": str(e)}, status=500)

        # Si AWS Lambda devuelve error, no guardamos en la base de datos
        if response.status_code != 200:
            return Response(response_data, status=400)

        # Guardar en la base de datos solo si la validación fue exitosa
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class TransactionSummaryView(APIView, RequireUserTokenMixin):
    def get(self, request, user_id):
        last_30_days = now().date() - timedelta(days=30)

        categories = Transaction.objects.filter(
            user_id=user_id, date__gte=last_30_days
        ).values("category").annotate(total=Sum("amount"))

        if not categories:
            return Response({"summary": "No hay transacciones en los últimos 30 días."})

        prompt = f"Resumen de gastos del usuario {user_id} en los últimos 30 días:\n"
        for entry in categories:
            prompt += f"- {entry['category']}: ${entry['total']:.2f}\n"

        prompt += "Analiza los gastos y da una recomendación."

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )

        return Response({"summary": response['choices'][0]['message']['content']})
