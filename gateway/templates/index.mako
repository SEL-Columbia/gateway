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

<ul class="index-list">
  <li><a href="/manage/show?class=Meter">Meters</a></li>
  <li><a href="/manage/show?class=CommunicationInterface">
      Communication Interfaces</a></li>
  <li><a href="/manage/show?class=TokenBatch">Tokens</a></li>
  <li><a href="/manage/pricing_models">Pricing Models</a></li>
</ul>


<ul class="index-list">
  <li><a href="/alerts/make">Manual alerts and test messages</a></li>
  <li><a href="/sms/index?limit=100">Check all SMS messages</a></li>
  <li><a href="/system/download">Download data tables</a></li>
</ul>
</%def>
