def get_main_html(data):
    logomark = '''
               <div id="logomark" class="padded-5px display-ib">
                <table>
                    <tr>
                        <td class="bg-color-white"></td>
                        <td class="bg-color-black"></td>
                        <td class="bg-color-white"></td>
                    </tr>
                    <tr>
                        <td class="bg-color-white"></td>
                        <td class="bg-color-white"></td>
                        <td class="bg-color-black"></td>
                    </tr>
                    <tr>
                        <td class="bg-color-white"></td>
                        <td class="bg-color-black"></td>
                        <td class="bg-color-white"></td>
                    </tr>
                </table>
            </div>
   '''

    logotype = '''
            <div id="logotype" class="display-ib">
                kompjuut [alpha]
            </div>
    '''
    nav = f'''
         <div id="nav" class="display-flex padded-15px margin-auto max-width-600px">
           {logomark}
           {logotype}
        </div>
    '''
    header = f'''
         <div id="header" class="bg-color-black">
           {nav}
         </div>
    '''

    content = '''
       <div id="content" class="padded-15px margin-auto max-width-600px">
            <div id="chat">
            </div>
        </div>
    '''

    html = f'''
       {header}
       {content}
    '''

    return html
