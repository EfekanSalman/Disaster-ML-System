from pydantic import BaseModel, Field
from typing import List
from datetime import date

# Zaman Serisi API'sinin ne alıp ne vereceğini tanımlar

class TimeSeriesInput(BaseModel):
    """
    Kullanıcıdan "Gelecekte kaç ay sonrasını
    tahmin etmemi istiyorsun?" bilgisini alır.
    """
    periods_to_forecast: int = Field(
        default=12,
        gt=0, # 0'dan büyük olmalı
        description="Geleceğe yönelik tahmin edilecek ay sayısı."
    )

class ForecastItem(BaseModel):
    """
    Tahminin her bir satırını (Ay + Tahmin) temsil eder.
    """
    date: date
    predicted_count: float

class TimeSeriesOutput(BaseModel):
    """
    API'nin döneceği tam yanıt.
    Model sürümünü ve tahminlerin BİR LİSTESİNİ içerir.
    """
    model_version: str = Field(..., example="timeseries_model_v1")
    forecast: List[ForecastItem]