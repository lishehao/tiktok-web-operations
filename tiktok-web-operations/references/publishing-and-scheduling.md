# Publishing And Scheduling

## Web capability baseline

Do not hard-code upload limits. Recheck the live UI because TikTok changes limits and regional eligibility. On 2026-07-10, the live `@shehaolili` upload page showed a maximum of `30 GB / 60 minutes`, recommended MP4, recommended 1080p/1440p/4K, and recommended 9:16 or 16:9. This already differed from an older TikTok support-page snapshot, so the account's current upload UI is authoritative.

The web uploader uploads the complete file; trimming may require the app.

TikTok Studio may expose upload, schedule, post management, comment management, analytics, cover selection, caption, audience, interaction settings, and copyright checking. Treat only visible controls as available.

## Publish packet

Prepare one packet per video:

- Local file path and provenance.
- Duration, format, resolution, orientation, and size.
- Content pillar, audience, region/language, hypothesis, and desired viewer action.
- Hook, shot sequence, on-screen text, voiceover, caption, hashtags, mentions, cover, and link plan.
- Music/sound rights and copyright-check result.
- Commercial disclosure and AIGC disclosure decisions.
- Visibility, comments, Duet, Stitch, sticker, Story, and privacy settings.
- Publish now or exact local schedule time/timezone.

## Action sequence

1. Validate the local asset before opening the upload flow.
2. Compare the packet with recent account history and the current live trend/context.
3. Run Check A and produce the final exact packet.
4. Request action-time confirmation for the packet.
5. Upload one video and wait for the page to parse it.
6. Apply only the confirmed settings.
7. Run Check B, including copyright and disclosure state.
8. Submit or schedule once.
9. Verify in TikTok Studio Posts, the schedule list, or the public profile.
10. Store the resulting URL/status and processing state in the ledger.

If any confirmed field changes materially, stop and reconfirm before submission.

## Quality rules

- Do not mechanically copy a trend. Preserve the trend's recognizable grammar while giving it a Loci-native payoff.
- Prefer original screen recordings, product footage, creator narration, location footage with permission, or clearly transformed assets.
- Avoid identical openings, captions, hashtag bundles, covers, or footage order across adjacent posts.
- Use hashtags for discovery context, not as a substitute for a clear hook or caption.
- A post may be scheduled only when its asset, rights, disclosure, and settings are fully ready.
