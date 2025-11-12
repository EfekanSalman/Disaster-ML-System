from pydantic import BaseModel, Field
from typing import List  # List'i import ediyoruz


# --- Problem 1 (Regresyon) için Şemalar (DEĞİŞMEDİ) ---

class DamagePredictionInput(BaseModel):
    """
    Problem 1 (/predict) için API girdi şeması.
    """
    Disaster_Subgroup: str = Field(..., alias="Disaster Subgroup", example="Hydrological")
    Continent: str = Field(..., example="Asia")
    Disaster_Group: str = Field(..., alias="Disaster Group", example="Natural")

    Total_Deaths: float = Field(..., alias="Total Deaths", example=100.0)
    No_Injured: float = Field(..., alias="No Injured", example=50.0)
    No_Affected: float = Field(..., alias="No Affected", example=1000.0)
    Dis_Mag_Value: float = Field(..., alias="Dis Mag Value", example=7.5)
    Start_Year: int = Field(..., alias="Start Year", example=2024)

    class Config:
        populate_by_name = True


class DamagePredictionOutput(BaseModel):
    """
    Problem 1 (/predict) için API çıktı şeması.
    """
    log_damage_prediction: float = Field(..., example=5.86)
    estimated_damage_usd_thousands: float = Field(..., example=73573.12)
    model_version: str = Field(..., example="damage_model_v1")


# --- YENİ: Problem 2 (Sınıflandırma) için Şemalar ---

class ClassificationInput(BaseModel):
    """
    Problem 2 (/predict_subgroup) için API girdi şeması.

    Not: Bu model, Problem 1'den FARKLI özelliklerle
    eğitildi (örn: 'Dis Mag Value' KULLANILMADI).
    Bu yüzden şeması da farklıdır.
    """
    Continent: str = Field(..., example="Africa")
    Disaster_Group: str = Field(..., alias="Disaster Group", example="Natural")

    Total_Deaths: float = Field(..., alias="Total Deaths", example=50.0)
    No_Injured: float = Field(..., alias="No Injured", example=10.0)
    No_Affected: float = Field(..., alias="No Affected", example=500.0)
    Start_Year: int = Field(..., alias="Start Year", example=2024)

    class Config:
        populate_by_name = True


class ClassificationOutput(BaseModel):
    """
    Problem 2 (/predict_subgroup) için API çıktı şeması.
    """
    predicted_subgroup: str = Field(..., example="Climatological")
    model_version: str = Field(..., example="classification_model_v1")

    # İsteğe bağlı: Modelin tüm sınıflara verdiği olasılıkları da döndürebiliriz
    # probabilities: dict = Field(..., example={"Hydrological": 0.2, "Climatological": 0.8})