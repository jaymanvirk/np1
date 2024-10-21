def get_main_html(data):
    logomark = '''
               <div id="logomark" class="padded-5px display-ib">
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
            <div id="logotype" class="display-ib">
                kompjuut [alpha]
            </div>
    '''

    header = f'''
         <div id="header">
            <div id="nav" class="bg-white padded-15px margin-auto max-width-600px">
           {logomark}
           {logotype}
           </div>
       </div>
    '''

    content = '''
       <div id="content" class="padded-15px margin-auto max-width-600px">
            <div id="chat_log">
            </div>
        </div>
    '''

    html = f'''
       {header}
       {content}
    '''

    return html
