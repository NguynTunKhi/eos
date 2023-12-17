class Response:
    def __init__(self, code, message, data, total=None, page=None, page_size=None):
        self.code = code
        self.message = message
        self.data = data
        self.total = total
        self.page = page
        self.page_size = page_size

    def to_dict(self):
        meta = {
            "code": self.code,
            "message": self.message,
        }
        if self.page is not None:
            meta["page"] = self.page
        if self.page_size is not None:
            meta["page_size"] = self.page_size
        if self.total is not None:
            meta["total"] = self.total
        return {
            "meta": meta,
            "data": self.data
        }

BadRequest = Response(
    code=400,
    message="bad request",
    data=None
)
