from colorama import Fore, Style

BRIGHTYELLOW = '\u001b[93;1m'

ASCII_ART = {
    'day-drizzle': [
        f'   .-.    ',
        f'  (   ).  ',
        f' (___(__) ',
        f"{Fore.BLUE}.'.'.'.'  {Style.RESET_ALL}",
        f"{Fore.BLUE}.'.'.'.   {Style.RESET_ALL}",
    ],
    'night-drizzle': [
        f'{Fore.LIGHTBLACK_EX}   .-.    {Style.RESET_ALL}',
        f'{Fore.LIGHTBLACK_EX}  (   ).  {Style.RESET_ALL}',
        f'{Fore.LIGHTBLACK_EX} (___(__) {Style.RESET_ALL}',
        f"{Fore.BLUE}.'.'.'.'  {Style.RESET_ALL}",
        f"{Fore.BLUE}.'.'.'.   {Style.RESET_ALL}",
    ],
    'mist': [
        '_ - _ - _ -',
        '_ - _ - _  ',
        '_ - _ - _ -',
    ],
    'night-clear': [
        '     .-"--.   *',
        '+  /   ,’      ',
        '  |    |     @ ',
        '   \\    `.__.  ',
        '  * `-.__.-’   '
    ],
    'night-partial': [
        f'     .-"--.  * ',
        f'*  /   ,’      ',
        f"  |   '{Fore.LIGHTBLACK_EX}.--.   {Style.RESET_ALL}@",
        f'   \\{Fore.LIGHTBLACK_EX}.-(    ).  {Style.RESET_ALL}',
        f'   {Fore.LIGHTBLACK_EX}(___.__)__) {Style.RESET_ALL}'
    ],
    'night-partial-thunderstorm': [
        f'      .-"--.    *',
        f' *  /   ,’      ',
        f'   |    {Fore.LIGHTBLACK_EX}.--.   {Style.RESET_ALL}@',
        f'+   \\{Fore.LIGHTBLACK_EX}.-(    ).  {Style.RESET_ALL}',
        f'   *{Fore.LIGHTBLACK_EX}(___.__)__) {Style.RESET_ALL}',
        f'   {Fore.BLUE}‚‘{Style.RESET_ALL}//{Fore.BLUE}‚‘‚‘{Style.RESET_ALL}/{Fore.BLUE}‚‘‚‘{Style.RESET_ALL}',
        f'  {Fore.BLUE}‚‘‚{Style.RESET_ALL}//{Fore.BLUE}‘‚‘‚{Style.RESET_ALL}/{Fore.BLUE}‘‚‘ {Style.RESET_ALL}',
        f' {Fore.BLUE}‚‘‚{Style.RESET_ALL}/{Fore.BLUE}‘‚‘‚‘{Style.RESET_ALL}/{Fore.BLUE}‚‘   {Style.RESET_ALL}'
    ],
    'new-moon-north': [
        '*    .                ',
        '        *             ',
        "             '        ",
        '            .        *',
        '                  .   '
    ],
    'new-moon-south': [
        '           *      ',
        '                 .',
        "          *     ' ",
        '                  ',
        '   @            * '
    ],
    'day-partial': [
        f'{BRIGHTYELLOW}   \\  /     {Style.RESET_ALL}',
        f'{BRIGHTYELLOW}__ /¯¯{Style.RESET_ALL}.-.   ',
        f'{BRIGHTYELLOW}   \\_{Style.RESET_ALL}(   ). ',
        f'{BRIGHTYELLOW}   /{Style.RESET_ALL}(___(__)',
    ],
    'day-clear': [
        f'{BRIGHTYELLOW}   \\   /   {Style.RESET_ALL}',
        f'{BRIGHTYELLOW}    .-.    {Style.RESET_ALL}',
        f'{BRIGHTYELLOW}-- (   ) --{Style.RESET_ALL}',
        f'{BRIGHTYELLOW}    `-’    {Style.RESET_ALL}',
        f'{BRIGHTYELLOW}   /   \\   {Style.RESET_ALL}'
    ],
    'day-clouds': [
        '    .--.   ',
        ' .-(    ). ',
        '(___.__)__)',
    ],
    'night-clouds': [
        '           ',
        f'{Fore.LIGHTBLACK_EX}    .--.   {Style.RESET_ALL}',
        f'{Fore.LIGHTBLACK_EX} .-(    ). {Style.RESET_ALL}',
        f'{Fore.LIGHTBLACK_EX}(___.__)__){Style.RESET_ALL}',
        '           '
    ],
    'rain-partial': [
        f'{BRIGHTYELLOW}_`/¯¯{Style.RESET_ALL}.-.   ',
        f'{BRIGHTYELLOW} ,\\_{Style.RESET_ALL}(   ). ',
        f'{BRIGHTYELLOW}  /{Style.RESET_ALL}(___(__)',
        f'{Fore.BLUE}  ‚‘‚‘‚‘‚‘ {Style.RESET_ALL}',
        f'{Fore.BLUE}  ‚’‚’‚’‚  {Style.RESET_ALL}'
    ],
    'day-snow': [
        '   .-.   ',
        '  (   ). ',
        ' (___(__)',
        ' * * * * ',
        '* * * *  '
    ],
    'night-snow': [
        f'{Fore.LIGHTBLACK_EX}   .-.   {Style.RESET_ALL}',
        f'{Fore.LIGHTBLACK_EX}  (   ). {Style.RESET_ALL}',
        f'{Fore.LIGHTBLACK_EX} (___(__){Style.RESET_ALL}',
        ' * * * * ',
        '* * * *  '
    ],
    'snow-partial': [
        f'{BRIGHTYELLOW}_`/¯¯{Style.RESET_ALL}.-.   ',
        f'{BRIGHTYELLOW} ,\\_{Style.RESET_ALL}(   ). ',
        f'{BRIGHTYELLOW}  /{Style.RESET_ALL}(___(__)',
        f'   *  *  * ',
        f'  *  *  *  '
    ],
    'night-thunderstorm': [
        f'      {Fore.LIGHTBLACK_EX}.--.   {Style.RESET_ALL}',
        f'   {Fore.LIGHTBLACK_EX}.-(    ). {Style.RESET_ALL}',
        f'  {Fore.LIGHTBLACK_EX}(___.__)__){Style.RESET_ALL}',
        f' {Fore.BLUE}‚‘{Style.RESET_ALL}/{Fore.BLUE}‚‘‚{Style.RESET_ALL}/_{Fore.BLUE}‘‚‘ {Style.RESET_ALL}',
        f'{Fore.BLUE}‚‘‚{Style.RESET_ALL}/{Fore.BLUE}‘‚‘‚{Style.RESET_ALL}/{Fore.BLUE}‘   {Style.RESET_ALL}'
    ],
    'day-thunderstorm': [
        f'      .--.   ',
        f'   .-(    ). ',
        f'  (___.__)__)',
        f' {Fore.BLUE}‚‘{Style.RESET_ALL}/{Fore.BLUE}‚‘‚{Style.RESET_ALL}/_{Fore.BLUE}‘‚‘ {Style.RESET_ALL}',
        f'{Fore.BLUE}‚‘‚{Style.RESET_ALL}/{Fore.BLUE}‘‚‘‚{Style.RESET_ALL}/{Fore.BLUE}‘   {Style.RESET_ALL}'
    ],
    'night-rain': [
        f'{Fore.LIGHTBLACK_EX}   .-.   {Style.RESET_ALL}',
        f'{Fore.LIGHTBLACK_EX}  (   ). {Style.RESET_ALL}',
        f'{Fore.LIGHTBLACK_EX} (___(__){Style.RESET_ALL}',
        f'{Fore.BLUE}‚‘‚‘‚‘‚‘ {Style.RESET_ALL}',
        f'{Fore.BLUE}‚’‚’‚’‚  {Style.RESET_ALL}',
    ],
    'day-rain': [
        f'   .-.   ',
        f'  (   ). ',
        f' (___(__)',
        f'{Fore.BLUE}‚‘‚‘‚‘‚‘ {Style.RESET_ALL}',
        f'{Fore.BLUE}‚’‚’‚’‚  {Style.RESET_ALL}',
    ]
}
