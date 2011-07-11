<%inherit file="base.mako"/>

<%def name="header()">
<title>Manage home</title>
<script type="text/javascript">
  $(function() { 
      $(".index-list a").button();
  });
</script>
</%def>

<%def name="content()">
<table>
  <tr>
    <td>
      <ul class="index-list">
        <li><a href="${a_url}/manage/show_meters">Meters</a></li>
        <li><a href="${a_url}/manage/show?class=Circuit">Circuits</a></li>
        <li><a href="${a_url}/manage/show?class=Device">Devices</a></li>
        <ul>
          <li><a href="${a_url}/manage/show?class=KannelInterface">
              Communication Kannel</a></li>
          <li><a href="${a_url}/manage/show?class=NetbookInterface">
              Communication Netbook</a></li>       
        </ul> 
        <li><a href="${a_url}/manage/tokens">Tokens</a></li>
        <li><a href="${a_url}/manage/show?class=SystemLog">System Logs</a></li>
        <li><a href="${a_url}/manage/pricing_models">Pricing Models</a></li>
      </ul>
    </td>
    <td>
      <ul class="index-list">
        <li><a href="${a_url}/alerts/make">Manual alerts and test messages</a></li>
        <li><a href="${a_url}/sms/index?limit=100">Check all SMS messages</a></li>
        <li><a href="${a_url}/sms/meter_messages">Check all messages
        from meters</a></li>
        <li> 
          <a href="${a_url}/manage/show_alerts">View all system
            alerts</a></a>
        <li><a href="${a_url}/system/download">Download data tables</a></li>
      </ul>
      <hr /> 
      <h3>Manage and add users</h3>
      <ul class="index-list">        
        <li> <a href="${a_url}/user/add">Add a new user</a></li>
        <li> <a href="${a_url}/user/show">Manage users</a></li>
      </ul>      
    </td>
  </tr>
</table>
</%def>
