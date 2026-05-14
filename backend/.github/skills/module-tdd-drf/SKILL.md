---
name: module-tdd-drf
description: "Build new DRF modules with TDD. Use when creating new endpoints, serializers, and routes with explicit HTTP methods, retailer-only permissions, pagination, filters, external service validation, and Bruno collection updates."
argument-hint: "Module name + endpoints + permissions + inputs"
user-invocable: true
disable-model-invocation: false
---

# Module TDD for DRF

## When to Use
- Adding a new module or feature area with new endpoints
- You want feature tests first, then implementation
- You need explicit HTTP methods (no heavy Django magic)
- You must enforce permissions, ownership, and privacy
- You need pagination, filters, and external service validation
- You must keep Bruno collections in sync

## Inputs to Collect
- Module name and app folder(s)
- Endpoints and routes (including nesting and path params)
- Permissions (user type, ownership rules)
- Request body fields and validations
- External service calls and required fields
- Pagination and filter parameters
- Bruno collection updates (folder name and request names)

## Procedure
1. **Confirm routes and rules**
   - List endpoints and HTTP methods.
   - Confirm nesting and whether route params are ignored or enforced.
   - Confirm permission scope (e.g., retailer-only) and ownership checks.

2. **Write feature tests first**
   - Create tests mirroring current patterns in the repo.
   - Cover list pagination shape (`count`, `results`).
   - Cover permission failures (403) and ownership isolation (404 or empty).
   - Cover create validation (unique constraints, missing fields, bad external IDs).
   - Cover delete behavior (only delete item, leave shared resources intact).

3. **Add serializers with explicit methods**
   - Use explicit `validate_*`, `validate`, and `create`.
   - Prefer `SerializerMethodField` for computed fields (e.g., image URL).
   - Keep read-only fields explicit in `Meta.read_only_fields`.

4. **Implement views with explicit HTTP methods**
   - Prefer `APIView` or `GenericAPIView` with `get/post/delete` defined.
   - Resolve ownership based on authenticated user.
   - Apply filters explicitly in `get` if using `APIView`.
   - Apply pagination explicitly in `get`.
   - Handle external service validation in `post` and return clear errors.

5. **Wire URLs**
   - Add routes to the module `urls.py` and include in main `app/urls.py`.
   - Keep paths consistent with the existing API structure.

6. **Update Bruno collection**
   - Add a folder for the module following existing `collections` patterns.
   - Add requests for list, create, delete with proper auth inheritance.
   - Include pagination and filter query params in list requests.

7. **Verify**
   - Run module tests and any relevant subset.
   - Smoke test the list/create/delete endpoints.

## Decision Points
- **Route ownership**: Use URL params vs. resolve from current user.
- **Pagination**: Global vs. per-endpoint page size query param.
- **Filters**: Use `DjangoFilterBackend` or direct filterset in `APIView`.
- **External service**: Mock in tests and validate response fields.

## Quality Checks
- Tests cover success and permission/ownership errors.
- Pagination returns expected shape and honors query params if enabled.
- Filters apply to list results.
- Create rejects duplicates and invalid external IDs.
- Delete removes only the target record, not shared resources.
- Bruno collection matches endpoint paths and inputs.
