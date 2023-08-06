def rndwitherr(value, error, errdig=2, lowmag = -1, highmag = 2):
    '''
    This is similar in functionality to the error rounding function of the
    package [sigfig](https://github.com/drakegroup/sigfig). The difference
    is that it also switches between decimal notaton and scientific
    notation in an automatic manner. The default is the author's personal
    opinion of when this switch is done by most students. Decimal notation
    is used for numbers in the range 0.1 to 1000 by default. Outside this
    range the number is provided in scientific notation. Where this switch
    occurs can be set by optional parameters.

    The `sigfig` package is not used to avoid doing the exponent analysis for
    the switch between decimal and scientific notation twice. This also
    avoids having to convert strings to numbers.

    :param float value: is the value to be rounded.
    :param float error: is the error in the value to be rounded.
    :param int errdig: (default = 2) number of significant figures to keep on the error.
        The value is rounded to the least significant digit in the error.
    :param int lowmag: (default = -1) magnitude below which scientific
        notation is used.
    :param int highmag: (default = 2) magnitude above which scientific
        notation is used.

    :return string valuestr: rounded value.
    :return string errstr: rounded error.
    :return string pwroftenstr: string for scientific notation exponent. Empty string if
        values returned as decimals.

    Examples
    ========
    Default
    -------
    >>> from round_using_error import *
    >>> rndwitherr(12.345, 0.23)
    ('12.35', '0.23', '')
    >>> rndwitherr(983.4, 34)
    ('983', '34', '')
    >>> rndwitherr(1247.325, 1.23)
    ('1.2473', '0.0012', '3')
    >>> rndwitherr(0.2345, 0.0125)
    ('0.234', '0.013', '')
    >>> rndwitherr(0.0353, 0.00224)
    ('3.53', '0.22', '-2')
    >>> rndwitherr(3.353e-2,2.24e-3)
    ('3.35', '0.22', '-2')
    >>> rndwitherr(3.53e-2,2.24e-3)
    ('3.53', '0.22', '-2')
    >>> rndwitherr(83e-4, 0)
    ('8.300000000000', '0.000000000000', '-3')
    >>> rndwitherr(-2, 0.00034)
    ('-2.00000', '0.00034', '')
    >>> rndwitherr(0, 0.00034)
    ('0.00000', '0.00034', '')
    >>> rndwitherr(0, 3452)
    ('0', '3500', '')
    >>> rndwitherr(0.011,0.034)
    ('1', '3', '-2')
    >>> rndwitherr(0.011,0.34)
    ('1', '34', '-2')
    >>> rndwitherr(0.11,0.34)
    ('0.1', '0.3', '')
    >>> rndwitherr(1,34)
    ('1', '34', '')
    >>> rndwitherr(1,3437)
    ('1', '3437', '')
    >>> rndwitherr(12,3437)
    ('10', '3440', '')
    >>> rndwitherr(1222,343789)
    ('1', '344', '3')
    >>> rndwitherr(-2, -0.00034)
    Traceback (most recent call last):
      ...
    ValueError: Errors are expected to be >= 0.

    Adjusting the significant digits on errors
    ------------------------------------------
    >>> rndwitherr(1247.325, 1.23, errdig = 3)
    ('1.24733', '0.00123', '3')
    >>> rndwitherr(1247.325, 1.23, errdig = 1)
    ('1.247', '0.001', '3')

    Adjusting the cutoffs for switching to scientific notation
    ----------------------------------------------------------
    >>> rndwitherr(1247.325, 1.23, errdig = 1, highmag = 3)
    ('1247', '1', '')
    >>> rndwitherr(3.53e-2,2.24e-3, errdig = 1, lowmag = -2)
    ('0.035', '0.002', '')
    '''
    import math
    pwroften = 0
    if value != 0:
        pwroften = math.floor(math.log(math.fabs(value), 10))
    if error < 0:
        raise ValueError('Errors are expected to be >= 0.')
    if error == 0:
        rndto = int(pwroften - 12) # beyond this run up against 64 bit
        # precision
    if error > 0:
        if error < math.fabs(value) or value == 0:
            rndto = int(math.floor(math.log(error, 10) - errdig + 1))
        else:
            rndto = pwroften
    valscaled = value
    errscaled = error
    pwroftenstr = ''
    if (pwroften < lowmag) or (pwroften > highmag):
        valscaled = value * 10 ** (-pwroften)
        errscaled = error * 10 ** (-pwroften)
        rndto = rndto - pwroften
        pwroftenstr = str(pwroften)
    valscaled = round(valscaled, -rndto)
    errscaled = round(errscaled, -rndto)
    if rndto < 0:
        precisstr = '%.' + str(-rndto) + 'f'
    else:
        precisstr = '%.f'
    valuestr = str(precisstr % valscaled)
    errorstr = str(precisstr % errscaled)
    return valuestr, errorstr, pwroftenstr


def output_rndwitherr(value, error, errdig=2, lowmag = -1, highmag = 2,
                      style='latex'):
    r'''
    This method outputs the results of rndwitherr as a string. Accepts the
    same input as the method `rndwitherr()` and an additional optional
    parameter `style = "latex" or "text"` defining the output style of the
    returned string.

    :param float value:
    :param float error:
    :param int errdig: default = 2
    :param int lowmag: default = -1
    :param int highmag: default = 2
    :param string style: default = 'latex', alternative 'text'

    Examples
    ========
    >>> output_rndwitherr(3.53e-2,2.24e-3)
    '(3.53\\pm0.22)\\times 10^{-2}'
    >>> output_rndwitherr(3.53e-2,2.24e-3, style = "text")
    '(3.53 +/- 0.22) X 10^-2'
    >>> output_rndwitherr(3.53e-2,2.24e-3, errdig = 1, lowmag=-1, style = "text")
    '(3.5 +/- 0.2) X 10^-2'
    >>> output_rndwitherr(3.53e-2,2.24e-3, errdig = 1, lowmag=-2, style = "text")
    '0.035 +/- 0.002'
    >>> output_rndwitherr(3.53e-2,2.24e-3, errdig = 1, lowmag=-2, style = "string")
    Traceback (most recent call last):
      ...
    ValueError: style parameter must be either "latex" or "string".

    '''
    if style not in ('latex', 'text'):
        raise ValueError('style parameter must be either "latex" or "string".')
    valstr, errstr, expstr = rndwitherr(value, error, errdig, lowmag, highmag)
    pwrstr = ''
    lparen = ''
    rparen = ''
    if style == 'latex':
        pm = r'\pm'
    if style == 'text':
        pm = r' +/- '
    if expstr != '':
        lparen = '('
        rparen = ')'
        if style == 'latex':
            pwrstr = r'\times 10^{' + expstr + '}'
        if style == 'text':
            pwrstr = r' X 10^' + expstr
    return str(r'' + lparen + valstr + pm + errstr + rparen + pwrstr)

def latex_rndwitherr(value, error, errdig=2, lowmag = -1, highmag = 2):
    r'''
    This is a convenience function to render the output of `rndwitherr()`
    as a latex string. Equivalent to a call to `output_rndwitherr() with the
    style = "latex"`.
    :param float value:
    :param float error:
    :param int errdig: default = 2
    :param int lowmag: default = -1
    :param int highmag: default = 2
    :return str: latex representation

    Examples
    ========
    >>> latex_rndwitherr(3.53e-2,2.24e-3, errdig = 1, lowmag=-2)
    '0.035\\pm0.002'
    >>> latex_rndwitherr(3.53e-2,2.24e-3)
    '(3.53\\pm0.22)\\times 10^{-2}'
    >>> latex_rndwitherr(1247.325, 1.23)
    '(1.2473\\pm0.0012)\\times 10^{3}'

    To view in Jupyter latex output in Jupyter use:
    ```
    from IPython.display import Math
    Math(latex_rndwitherr(value, error))
    ```

    '''
    return output_rndwitherr(value, error, errdig, lowmag, highmag,
                             style='latex')

def text_rndwitherr(value, error, errdig=2, lowmag = -1, highmag = 2):
    '''
    This is a convenience function to render the output of `rndwitherr()`
    as a text string. Equivalent to a call to `output_rndwitherr() with the
    style = "text"`. `
    :param float value:
    :param float error:
    :param int errdig: default = 2
    :param int lowmag: default = -1
    :param int highmag: default = 2
    :return: string representation

    Examples
    ========
    >>> text_rndwitherr(3.53e-2,2.24e-3, errdig = 1, lowmag=-2)
    '0.035 +/- 0.002'
    >>> text_rndwitherr(3.53e-2,2.24e-3)
    '(3.53 +/- 0.22) X 10^-2'
    >>> text_rndwitherr(1247.325, 1.23)
    '(1.2473 +/- 0.0012) X 10^3'
    '''
    return output_rndwitherr(value, error, errdig, lowmag, highmag,
                             style='text')