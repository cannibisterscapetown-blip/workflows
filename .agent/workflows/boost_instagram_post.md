---
description: Boost an Instagram post as a Meta Ad for 7 days with R200 budget
---

1.  **Notify Agent**: Tell the agent "I made a new Instagram post" or "Boost the latest Instagram post".
2.  **Provide Post Details**: If not the latest, provide the specific Instagram Post ID or URL.
3.  **Agent Action**: The agent will run the `create_meta_ad.py` script.
    ```bash
    # Example command the agent will run
    python3 create_meta_ad.py --post_id <POST_ID>
    ```
4.  **Verification**: The agent will confirm the Ad Campaign, Ad Set, and Ad IDs created.
5.  **You're Done**: The ad is created in PAUSED state. You can review it in Ads Manager and enable it.

**Prerequisites**:
- Valid `META_ACCESS_TOKEN`, `META_AD_ACCOUNT_ID`, `META_PAGE_ID`, `META_INSTAGRAM_ACCOUNT_ID` in `.env`.
