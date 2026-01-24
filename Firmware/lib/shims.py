class UnifiedPin:
    """Wraps both native Pin and MCP VirtualPin to behave identically."""
    def __init__(self, pin_obj):
        self.obj = pin_obj
        self.is_virtual = (True if type(pin_obj) == "VirtualPin" else False)

    def value(self, val=None, pullup=False):
        if val is not None:
            # Writing
            if self.is_virtual: self.obj.output(val=val)
            else: self.obj.value(val)
        else:
            # Reading
            return self.obj.value() if not self.is_virtual else self.obj.input(pullup=pullup)

    def on(self): 
        self.value(val=1)
        
    def off(self): 
        self.value(val=0)