# core/branch_utils.py

def get_branch_id(request):
    """
    Pulls branch_id off the JWT payload attached by JWTMiddleware.
    Returns None if not present (e.g. super-admin with no branch).
    """
    user_data = getattr(request, "user_data", None)
    if not user_data:
        return None
    return user_data.get("branch_id")


def branch_queryset(request, model, **extra_filters):
    """
    Returns a queryset filtered to the logged-in user's branch.
    Assumes `model` has a `branch` FK (filtering on branch_id works
    whether the field is declared as `branch` or `branch_id`).
    Use this instead of Model.objects.all() in list/search views.
    """
    branch_id = get_branch_id(request)
    qs = model.objects.filter(**extra_filters)

    if branch_id is not None:
        qs = qs.filter(branch_id=branch_id)

    return qs