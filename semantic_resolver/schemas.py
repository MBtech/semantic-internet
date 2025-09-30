from typing import List, Optional, Dict
from pydantic import BaseModel, HttpUrl
from semantic_resolver.enums import (
    Category,
    Topic,
    Granularity,
    GeographicCoverage,
    TemporalCoverage,
    ContentType,
    DataFormat,
    QueryProtocol,
    AccessCost,
    AuthenticationMethod,
    License
)


# ===== Metadata Models =====

class ScopeMetadata(BaseModel):
    topics: List[Topic]
    granularity: Optional[Granularity] = None
    languages: List[str]
    geographic_coverage: Optional[GeographicCoverage] = None
    country_codes: Optional[List[str]] = None
    temporal_coverage: Optional[TemporalCoverage] = None


class ContentMetadata(BaseModel):
    content_types: List[ContentType]
    data_format: Optional[DataFormat] = None
    license: Optional[License] = None


class AccessMetadata(BaseModel):
    query_protocols: List[QueryProtocol]
    rate_limit: Optional[str] = None
    access_cost: Optional[AccessCost] = None
    authentication_required: Optional[List[AuthenticationMethod]] = None


class PerformanceMetadata(BaseModel):
    typical_latency_ms: Optional[int] = None
    worst_case_latency_ms: Optional[int] = None
    uptime_percentage: Optional[float] = None


class RelevanceMetadata(BaseModel):
    precision_score: Optional[float]
    recall_score: Optional[float] # Recall score for a k 
    trust_score: Optional[float]
    reputation_notes: Optional[str]


class SecurityMetadata(BaseModel):
    provenance: Optional[str] = None
    trustworthiness: Optional[str] = None
    privacy_constraints: Optional[str] = None


# ===== Main Model =====
class InformationSource(BaseModel):
    name: str
    description: str
    endpoint: HttpUrl
    category: Category

    scope: ScopeMetadata
    content: ContentMetadata
    access: AccessMetadata
    performance: Optional[PerformanceMetadata] = None
    relevance: Optional[RelevanceMetadata] = None
    security: Optional[SecurityMetadata] = None
    max_top_k: int = 10



class CategoryandTopic(BaseModel):
    category: Category
    topic: Topic