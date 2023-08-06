class FakeClass:
    """
    Fake class
    
    Attributes
    -----------
    name : str
        
    """
    
    def __init__(self, name=None):
        """
        Fake class
        
        Parameters
        -----------
        name : str
            if None name is set to "unknown"
        """
        
        if name is None:
            name = 'unknown'
        self.name = name

    def display(self, text=None):
        """
        Displays a text or name attribute if text is None
        
        Parameters
        -----------
        text : str
            if None, displays name (default=None)
        """
        
        if text is None:
            print(self.name)
        else:
            print(text)


def fake_function(text='Hello World!'):
    """ 
    Prints and returns a text after capitalizing
    
    Parameters
    ----------
    name : str
              
    Returns
    -------
    text: a text
    
    """

    text = text.capitalize()
    print(text)
    return text

