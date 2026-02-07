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
            # handle polarity
            if not self.is_virtual and pullup:
                return not self.obj.value() # invert for pullup
            elif not self.is_virtual and not pullup:
                return self.obj.value() 
            else: # virtual pins handle pullup internally
                #return self.obj.input(pullup=pullup)
                return self.obj.input()

    def on(self): 
        self.value(val=1)
        
    def off(self): 
        self.value(val=0)