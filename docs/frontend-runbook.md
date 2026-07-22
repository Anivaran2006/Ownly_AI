# Frontend Runbook

## Local Startup

```bash
npm install
npm run dev --workspace @ownly/web
```

Open http://localhost:3000.

## Implemented Surfaces

- `/`: dashboard with scanner preview, KPIs, warranty radar, AI search card, product list, resale card, and family workspace.
- `/scanner`: AI receipt scanner review surface.
- `/products`: product profile list and selected profile view.
- `/login`: auth/onboarding surface.
- `/settings`: security and integration controls.

## Next UI Wiring

- Replace `lib/sample-data.ts` with API calls from `lib/api-client.ts`.
- Persist login tokens with secure HTTP-only cookies from the API.
- Add route protection and workspace switching.
- Add upload progress and server-sent scan events.
- Add chart components once real analytics endpoints are populated.

