"""
Cannabis ad compliance checker for Google Ads.

Google prohibits ads for cannabis/marijuana products globally.
Cannibisters runs ads exclusively for social club membership (cannibisters.co.za),
not for product sales. This module enforces that boundary and catches policy risks
before ads are submitted to Google.

Risk levels:
  BLOCKED  — will definitely be disapproved, do not submit
  HIGH     — very likely to be disapproved
  MEDIUM   — review manually before submitting
  LOW      — minor concern, note and proceed
  CLEAR    — no issues detected
"""

from dataclasses import dataclass, field
from typing import List


# Terms that will trigger immediate disapproval
BLOCKED_TERMS = [
    "cannabis", "marijuana", "weed", "thc", "dagga", "ganja", "420", "kush",
    "bud", "flower", "hash", "hashish", "cbd oil", "cbd products", "buy cbd",
    "dispensary", "online dispensary", "cannabis store", "cannabis shop",
    "buy weed", "buy cannabis", "buy marijuana", "cannabis delivery",
    "cannabis for sale", "marijuana for sale", "weed for sale",
    "recreational cannabis", "cannabis products", "cbd capsules",
    "hemp flower", "pre-rolls", "pre roll", "joint", "blunt", "dab",
    "concentrate", "edibles", "vape cartridge", "cannabis vape",
    "thc vape", "weed vape", "cannabis oil", "cbd cream for sale",
]

# Terms that are medium-risk — okay in some contexts but flag for review
MEDIUM_RISK_TERMS = [
    "herbal remedy", "herbal supplement", "natural high", "smoking",
    "smoke", "herb", "botanical extract", "plant medicine",
    "alternative medicine", "holistic", "wellness", "relaxation",
    "stress relief",
]

# Prohibited landing page patterns — paths that indicate a product store
BLOCKED_URL_PATTERNS = [
    "/products", "/shop", "/store", "/buy", "/cart", "/checkout",
    "/collections", "/product/", "cannibisters.com",
]

# Safe, recommended terms for Cannibisters membership ads
SAFE_TERMS = [
    "social club", "private members club", "exclusive membership",
    "members only", "join our community", "apply for membership",
    "herbal apothecary", "apothecary", "community", "lifestyle",
    "cannibisters", "cannibisters.co.za", "club membership",
    "exclusive club", "private club", "members experience",
]

# Compliant headline options (≤30 chars each for RSA)
COMPLIANT_HEADLINES = [
    "Join Our Social Club",           # 21 chars
    "Cannibisters Social Club",       # 25 chars
    "Members-Only Experience",        # 23 chars
    "Apply for Membership Today",     # 27 chars
    "Cape Town's Herbal Club",        # 24 chars
    "Exclusive Herbal Community",     # 26 chars
    "Private Members Club SA",        # 23 chars
    "Become a Member Today",          # 21 chars
    "Cannibisters - Join Now",        # 23 chars
    "The Apothecary Social Club",     # 27 chars
    "Members Club - Apply Now",       # 24 chars
    "Herbal Apothecary Members",      # 25 chars
]

# Compliant description options (≤90 chars each for RSA)
COMPLIANT_DESCRIPTIONS = [
    "Join Cannibisters Social Club. Exclusive herbal apothecary experience. Apply today.",
    "Private members club for herbal apothecary enthusiasts. Limited spots. Sign up now.",
    "Cannibisters Social Club — Cape Town's premier private members community. Join us.",
    "Exclusive membership access. Cannibisters Herbal Apothecary community. Apply online.",
    "Members-only access to South Africa's leading herbal apothecary social club.",
    "Join the Cannibisters community. Private social club membership. Limited availability.",
]

# Compliant negative keywords to add to every campaign
NEGATIVE_KEYWORDS = [
    "buy", "purchase", "order", "shop", "store", "cheap", "discount",
    "free", "delivery", "online dispensary", "cannabis products",
    "marijuana products", "thc products", "cbd products", "cannabis oil",
    "weed", "dagga", "ganja", "hash", "pre roll", "edibles", "vape",
    "concentrate", "dab", "blunt", "flower", "bud", "strain",
    "indica", "sativa", "hybrid",
]

# Safe keyword suggestions for search campaigns
RECOMMENDED_KEYWORDS = {
    "EXACT": [
        "[social club membership cape town]",
        "[herbal social club south africa]",
        "[cannibisters social club]",
        "[cannibisters membership]",
        "[private members club cape town]",
        "[exclusive club membership south africa]",
    ],
    "PHRASE": [
        '"social club membership"',
        '"herbal social club"',
        '"private members club"',
        '"exclusive members club"',
        '"herbal apothecary"',
        '"cannabis social club"',
        '"social club cape town"',
        '"members only club south africa"',
    ],
    "BROAD_MATCH_MODIFIER": [
        "+social +club +membership +cape +town",
        "+herbal +apothecary +membership",
        "+exclusive +members +club +south +africa",
        "+private +social +club +johannesburg",
    ],
}


@dataclass
class ComplianceResult:
    risk_level: str          # BLOCKED / HIGH / MEDIUM / LOW / CLEAR
    issues: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    blocked_terms_found: List[str] = field(default_factory=list)
    medium_risk_terms_found: List[str] = field(default_factory=list)

    @property
    def is_safe_to_submit(self) -> bool:
        return self.risk_level not in ('BLOCKED', 'HIGH')


def check_text(text: str) -> ComplianceResult:
    """Check ad headline or description text for policy violations."""
    lower = text.lower()
    result = ComplianceResult(risk_level='CLEAR')

    for term in BLOCKED_TERMS:
        if term in lower:
            result.blocked_terms_found.append(term)

    for term in MEDIUM_RISK_TERMS:
        if term in lower:
            result.medium_risk_terms_found.append(term)

    if result.blocked_terms_found:
        result.risk_level = 'BLOCKED'
        result.issues.append(
            f"Prohibited terms found: {', '.join(result.blocked_terms_found)}"
        )
        result.suggestions.append(
            "Replace product/drug references with membership language. "
            "See COMPLIANT_HEADLINES and COMPLIANT_DESCRIPTIONS for safe copy."
        )
    elif result.medium_risk_terms_found:
        result.risk_level = 'MEDIUM'
        result.issues.append(
            f"Medium-risk terms — review before submitting: "
            f"{', '.join(result.medium_risk_terms_found)}"
        )
    else:
        result.risk_level = 'CLEAR'

    return result


def check_url(url: str) -> ComplianceResult:
    """Check that the landing page URL is the membership site, not the product store."""
    result = ComplianceResult(risk_level='CLEAR')
    lower = url.lower()

    for pattern in BLOCKED_URL_PATTERNS:
        if pattern in lower:
            result.risk_level = 'BLOCKED'
            result.issues.append(
                f"Landing page URL contains '{pattern}'. "
                f"Google Ads must never point to the product store or product pages."
            )
            result.suggestions.append(
                f"Use {MEMBERSHIP_URL_HINT} as the landing page instead."
            )
            break

    if 'cannibisters.co.za' not in lower and result.risk_level == 'CLEAR':
        result.risk_level = 'MEDIUM'
        result.issues.append(
            "Landing page is not cannibisters.co.za — confirm this is intentional."
        )

    return result


MEMBERSHIP_URL_HINT = "https://www.cannibisters.co.za (or /join page)"


def check_ad(headlines: List[str], descriptions: List[str], final_url: str) -> ComplianceResult:
    """Full compliance check for a responsive search ad."""
    combined = ComplianceResult(risk_level='CLEAR')

    all_texts = headlines + descriptions
    for text in all_texts:
        r = check_text(text)
        combined.blocked_terms_found.extend(r.blocked_terms_found)
        combined.medium_risk_terms_found.extend(r.medium_risk_terms_found)
        combined.issues.extend(r.issues)
        combined.suggestions.extend(r.suggestions)

    url_result = check_url(final_url)
    combined.issues.extend(url_result.issues)
    combined.suggestions.extend(url_result.suggestions)

    # Remove duplicates
    combined.blocked_terms_found = list(set(combined.blocked_terms_found))
    combined.medium_risk_terms_found = list(set(combined.medium_risk_terms_found))
    combined.issues = list(dict.fromkeys(combined.issues))
    combined.suggestions = list(dict.fromkeys(combined.suggestions))

    if combined.blocked_terms_found or url_result.risk_level == 'BLOCKED':
        combined.risk_level = 'BLOCKED'
    elif combined.medium_risk_terms_found or url_result.risk_level == 'MEDIUM':
        combined.risk_level = 'MEDIUM'
    else:
        combined.risk_level = 'CLEAR'

    return combined


def print_compliance_report(result: ComplianceResult, label: str = "Ad"):
    icons = {'BLOCKED': 'BLOCKED', 'HIGH': 'HIGH', 'MEDIUM': 'MEDIUM', 'LOW': 'LOW', 'CLEAR': 'CLEAR'}
    print(f"\n[{icons.get(result.risk_level, result.risk_level)}] {label}")
    if result.issues:
        for issue in result.issues:
            print(f"  Issue: {issue}")
    if result.suggestions:
        for s in result.suggestions:
            print(f"  Suggestion: {s}")
    if result.risk_level == 'CLEAR':
        print("  No policy issues detected.")
    print(f"  Safe to submit: {'Yes' if result.is_safe_to_submit else 'No'}")
