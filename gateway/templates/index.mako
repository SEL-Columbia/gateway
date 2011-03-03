<%inherit file="base.mako"/>

<%def name="header()">
   <title>Dashboard SharedSolar Gateway</title>

   <script type="text/javascript">
     $(function() { 
        $('.button').button(); 
        $('.widgets').setWidget('.widget');
     }); 

   </script>

</%def>

<%def name="content()">


% if logged_in:
<div class="widgets"> 

<div id="manage-meter" class="widget">
  <div class="widget-header">Manage meters</div>
  <div class="widget-content">
  <p><a class="button" 
        href="${request.application_url}/add/Meter"> 
      Add a new meter</a></p>
  ${meters.render()}
 </div>
</div>

<div id="manage-messages" class="widget">
<div class="widget-header">Manage and send SMS Messages</div>
<div class="widget-content">

<a class="button"
      href="${request.application_url}/sms/index?limit=100"> Check all
      SMS messages</a> </li>
<a class="button" href="${request.application_url}/alerts/make"> Send an
      alert or test message</a>
</div> 
</div>


<div id="manage-interface" class="widget">
  <div class="widget-header">Manage Interfaces</div>
  <div class="widget-content">
    <p><a class="button"
            href="${request.application_url}/add/KannelInterface">
        Add kannel interface</a>
      <a class="button"
         href="${request.application_url}/add/NetbookInterface">
        Add netbook interface</a></p>
  ${interfaces.render()}
  </div>
</div>

<div id="manage-token" class="widget"> 
  <div class="widget-header">Manage tokens</div>
  <div class="widget-content">
  <form method="POST" id=""
        action="${request.application_url}/add_tokens">
    <table>
      <tr>
        <td class="hint">Number of tokens to be create</td>
        <td><input type="text" name="amount" value="" /></td>
      </tr>
      <tr>
        <td class="hint">Value for each token</td>
        <td><input type="text" name="value" value="" /></td>
      </tr>
      <tr>
        <td></td>
        <td><input class="button" 
                   type="submit" 
                   name="" 
                   value="Add token" /></td>
      </tr>
    </table>
  </form>
  <h4>Upload tokens from csv</h4>
  <form method="POST" id=""
        enctype="multipart/form-data"
        action="${request.application_url}/upload_tokens">
    <input type="file" name="csv" value="" />
    <input class="button" 
           type="submit" 
           name="submit" 
           value="Upload tokens from csv" />
  </form>
  <h4>Existing token batches</h4>
  <table>    
    <tr>
      <th>Batch uuid</th>
      <th>Batch id</th>
      <th>Batch created on</th>
      <th>Number of tokens in batch</th>
      <th></th>
    </tr>
  % for batch in tokenBatchs:   
    <tr>
      <td><a href="${batch.getUrl()}">${batch.uuid}</a></td>
      <td>${str(batch.id)}</td>
      <td>${batch.created.ctime()}</td>
      <td>${str(batch.get_tokens().count())}</td>
      <td><a href="${request.application_url}/token/export_batch/${batch.uuid}">
          Export batch to CSV</a></td>
    </tr>
  % endfor 
  </table>
</div>
</div>

<div id="manage-system-logs" class="widget">
  <div class="widget-header" >Manage and view system logs</div>
  <div class="widget-content">
    ${logs.render()}
  </div>
</div>

% else: 
% endif

</div>
</%def>
