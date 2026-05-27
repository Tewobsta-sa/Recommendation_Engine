from pydantic import BaseModel  
from typing import List, Optional, Literal, Dict  


class Preferences(BaseModel):  
    curriculum: Optional[str] = None  
    min_budget: Optional[float] = None  
    max_budget: Optional[float] = None  
    distance_km: float = 25.0  
    lat: Optional[float] = None  
    lng: Optional[float] = None 
    school_type: Optional[Literal["private", "government", "church"]] = None 
    school_level: Optional[str] = None  


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
    school_type: Optional[Literal["private", "government", "church"]] = None 
    passing_rate: Optional[float] = None
    national_exam_score: Optional[float] = None
    
    # New fields
    total_students: Optional[int] = None
    girls_count: Optional[int] = None
    boys_count: Optional[int] = None
    gender_balance_index: Optional[float] = None
    academic_year: Optional[int] = None
    achievement_score: Optional[float] = None
    achievement_count: Optional[int] = None
    recent_achievement_year: Optional[int] = None
    staff_quality_score: Optional[float] = None
    staff_breakdown: Optional[List[Dict]] = None
    follower_count: Optional[int] = None
    review_count: Optional[int] = None
    total_achievement_score: Optional[float] = None

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
