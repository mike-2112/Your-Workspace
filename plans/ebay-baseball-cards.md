# eBay Baseball Cards Listings Plan (1975 cards)

## Overview
Mike wants to list 1975 baseball cards on eBay. He'll provide photos via Google Drive access.

## Required eBay Setup (One-Time)
1. **Developer Account**: eBay Developers Program (free). Create app for Production keys.
2. **OAuth 2.0 Auth**:
   - Client ID/Secret (App ID/Cert ID).
   - Scopes: https://api.ebay.com/oauth/api_scope/sell.inventory https://api.ebay.com/oauth/api_scope/sell.marketing (etc. for listings/offers).
   - User consent flow: Redirect URI, get code, exchange for access_token (expires 2h, refresh_token for long-term).
3. **Sandbox Testing**: Test in Sandbox before Production.

## Key APIs (Sell APIs v1.1+)
- **Inventory API**: Create/manage inventory items (product details: title, description, condition, category, format: FIXED_PRICE or AUCTION).
  - POST /sell/inventory/v1/inventory_item/{sku}
- **Offer API**: Create offers linked to inventory (price, quantity, listing policies).
  - POST /sell/inventory/v1/offer
  - Publish: POST /sell/inventory/v1/offer/{offerId}/publish → gets listingId.
- **Image Upload**: 
  - Upload images to eBay via File Exchange API or directly in Offer (imageUrls).
  - For Google Drive: Download images via Drive API, upload to eBay.
- **Account API**: Shipping/payment policies.
- **Taxonomy API**: Find category IDs (Sports Mem > Baseball Cards).

## Full Flow for One Listing
1. Create Inventory Item (SKU unique, e.g. '1975-topps-card-001').
2. Create Offer (link SKU, price, images, category).
3. Publish Offer → Live listing.

## Bulk: 
- Use Inventory API bulk endpoints or loop.

## Tools Needed
- Node.js/Python script with ebay-node-api or requests.
- Google Drive API: Service account or OAuth for access.
- Store tokens securely (env vars, not code).

## Risks/Notes
- eBay fees, policies (condition grading accurate).
- Auth tokens: Secure storage.
- Rate limits: 5k calls/day Production.
- Test: Sandbox account.

Awaiting: eBay app credentials, Google Drive access, card details/photos, SKUs/prices.

Updated: 2026-03-15