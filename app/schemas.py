from pydantic import BaseModel  
from typing import List, Optional, Literal  
  
  
class Preferences(BaseModel):  
    curriculum: Optional[str] = None  
    min_budget: Optional[float] = None  
    max_budget: Optional[float] = None  
    distance_km: float = 25.0  
    lat: Optional[float] = None  
    lng: Optional[float] = None  
  
  
class School(BaseModel):  
    id: int  
    name: str  
    curriculum: str  
    tuition_fee: float  
    rating: float  
    facilities: str  
    verification_status: str  
    latitude: float  
    longitude: float  
    school_level: Optional[str] = None 

    class Config:  
        extra = "allow"
  
  
class RecommendationRequest(BaseModel):  
    parent_id: Optional[int] = None  
    preferences: Preferences  
    schools: List[School]  
  
  
class FeedbackRequest(BaseModel):

    recommendation_id: Optional[int] = None

    parent_id: int

    school_id: int

    result: str