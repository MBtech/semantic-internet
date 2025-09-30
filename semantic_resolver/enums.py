from enum import Enum

# ===== Enums =====
class Category(str, Enum):
    news_site = "news_site"
    entertainment = "entertainment"
    wiki = "wiki"
    education = "education"
    travel = "travel"
    marketplace = "marketplace"
    ecommerce = "ecommerce"
    social_media = "social_media"
    research = "research"
    forum = "forum"
    census = "census"
    blog = "blog"
    video = "video_platform"
    reference = "reference"
    corportate = "corporate_site"
    other = "other"

class Topic(Enum):
    NEWS = "News & Current Affairs"
    POLITICS = "Politics & Government"
    BUSINESS = "Business & Finance"
    TECHNOLOGY = "Technology & Innovation"
    SCIENCE = "Science & Research"
    HEALTH = "Health & Medicine"
    EDUCATION = "Education & Learning"
    ENVIRONMENT = "Environment & Sustainability"
    SPORTS = "Sports & Athletics"
    ENTERTAINMENT = "Entertainment & Media"
    ART_CULTURE = "Art, Culture & Humanities"
    LIFESTYLE = "Lifestyle & Wellness"
    TRAVEL = "Travel & Tourism"
    FOOD = "Food & Culinary"
    RELIGION_SPIRITUALITY = "Religion & Spirituality"
    HISTORY = "History & Heritage"
    LAW_CRIME = "Law, Crime & Justice"
    SOCIETY = "Society & Social Issues"
    ECONOMY = "Economy & Trade"
    GENERAL = "General"
    OTHER = "Other / Miscellaneous"



class Granularity(str, Enum):
    broad = "broad"
    specialized = "specialized"


class GeographicCoverage(str, Enum):
    local = "local"
    national = "national"
    international = "international"
    regional = "regional"

class License(str, Enum):
    public_domain = "public_domain"
    cc_by = "CC-BY"
    cc_by_sa = "CC-BY-SA"
    cc_by_nd = "CC-BY-ND"
    cc_by_nc = "CC-BY-NC"
    cc_by_nc_sa = "CC-BY-NC-SA"
    cc_by_nc_nd = "CC-BY-NC-ND"
    gpl = "GPL"
    mit = "MIT"
    apache_2_0 = "Apache-2.0"
    proprietary = "proprietary"
    other = "other"

class TemporalCoverage(str, Enum):
    current = "current"
    recent_decades = "recent_decades"
    historical = "historical"
    all = "all"


class ContentType(str, Enum):
    article = "article"
    text = "text"
    book = "book"
    dataset = "dataset"
    database = "database"
    image = "image"
    video = "video"
    audio = "audio"
    code = "code"
    blog_post = "blog_post"
    other = "other"


class DataFormat(str, Enum):
    structured = "structured"
    unstructured = "unstructured"
    semi_structured = "semi_structured"


class QueryProtocol(str, Enum):
    rest = "rest"
    graphql = "graphql"
    sparql = "sparql"
    sql = "sql"
    other = "other"


class AccessCost(str, Enum):
    free = "free"
    subscription = "subscription"
    pay_per_use = "pay_per_use"
    other = "other"


class AuthenticationMethod(str, Enum):
    none = "none"
    api_key = "api_key"
    oauth = "oauth"
    token = "token"
    other = "other"
