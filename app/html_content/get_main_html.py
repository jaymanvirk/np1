def get_main_html(data):
    logomark = '''
             <div id="logomark">
                <table>
                    <tr>
                        <td class="bg-black"></td>
                        <td class="bg-white"></td>
                        <td class="bg-black"></td>
                    </tr>
                    <tr>
                        <td class="bg-black"></td>
                        <td class="bg-black"></td>
                        <td class="bg-white"></td>
                    </tr>
                    <tr>
                        <td class="bg-black"></td>
                        <td class="bg-white"></td>
                        <td class="bg-black"></td>
                    </tr>
                </table>
            </div>
    '''

    logotype = '''
            <div id="logotype">
                kompjuut
            </div>
    '''

    header = f'''
         <div id="header" class="fixed top">
           {logomark}
           {logotype}
       </div>
    '''

    main = '''
        <div id="main">
            <div id="chat_log">
            </div>
        </div>
    '''

    html = f'''
       {header}
       {main}
    '''

    return html
