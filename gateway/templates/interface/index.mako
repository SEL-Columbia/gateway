<%inherit file="../base.mako"/>

<%def name="header()">
  <title>Interface page</title>
  <script type="text/javascript">
    $(function() { 
       $(".button").button();
    });
  </script>
</%def>

<%def name="content()">    
    <a class="button"
       href="${request.application_url}/edit/${type(interface).__name__}/${interface.id}">
      Edit</a> 
    <a class="button"
       href="${request.application_url}/interface/remove/${interface.id}">
      Remove</a>
    <hr />

    <table>
      % for key,value in fields.iteritems(): 
      <tr>
        <td class="hint">Interface ${key}</td>
        <td>${value.get("value")}</td>
      </tr>
      % endfor 
    </table>

</%def>
