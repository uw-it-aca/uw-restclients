
class MockHTTP(object):
    status = 0
    body = ""
    def read(self):
        return self.body
