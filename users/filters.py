
def apply_user_filters(users, request):
    name = request.query_params.get("name")
    is_active_param = request.query_params.get("is_active")
    active_values = {"true": True, "false": False}

    if is_active_param is not None and is_active_param not in active_values:
        return None
    if is_active_param is not None:
        users = users.filter(is_active=active_values[is_active_param])

    if name is not None:
        name = name.strip()
        if name:
            users = users.filter(name__icontains=name)
    return users


def apply_department_filter(users, request):
    department = request.query_params.get("department")
    
    if department is None:
        return users
    
    try:
        department_id = int(department)
    except (ValueError, TypeError):
        return None
    
    if department_id < 1:
        return None
    
    users = users.filter(department_id = department_id)
    
    return users


def apply_user_ordering(users, request):
    allowed_ordering = ["age", "-age", "name", "-name"]
    ordering = request.query_params.get("ordering")

    if ordering is not None and ordering not in allowed_ordering:
        return None
    if ordering is not None:
        users = users.order_by(ordering)

    return users


def apply_min_age_filter(users, request):
    min_age = request.query_params.get("min_age")

    if min_age is None:
        return users

    try:
        min_age = int(min_age)
    except (ValueError, TypeError):
        return None

    if min_age < 0:
        return None

    users = users.filter(age__gte=min_age)

    return users

