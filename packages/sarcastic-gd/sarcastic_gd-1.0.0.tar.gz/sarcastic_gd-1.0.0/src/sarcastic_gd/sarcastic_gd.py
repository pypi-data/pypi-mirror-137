from random import choice

def sarcastic_gd(func):
    """
    Transforms a normal boring gradient descent function into once which
    will say hurtful things in a sarcastic tone.

    Params:
        func:function
            The function to be decorated
    Returns:
        wrapper:function
            A wrapper around func which makes SGD far more interesting
    """
    def wrapper(*args, **kwargs):
        sarcasms = [
            "This'll totally converge...",
            "Your statistical model is SOOooo good...",
            "Oh yeah. Your learning rate is great. Not too big at all.",
            "You chose *that* model? I don't see ANY issue with that decision...",
            "ERROR: 1,000,000",
            "Are you sure training this model is a good use of your time?",
            "Just because you watched a video on youtube doesn't mean you\
                    understand machine learning."
        ]
        sarcastic_remark = choice(sarcasms)
        func_output = func(*args, **kwargs)
        print(sarcastic_remark)
        return func_output

    return wrapper
