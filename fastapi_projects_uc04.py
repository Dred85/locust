def open_projects(user):
    user.client.get("/projects")