<%inherit file="../base.mako"/>
<%namespace name="headers" file="../headers.mako"/>

<%def name="header()">
<style type="text/css" media="screen">
  td { 
  border: none;
} 
</style>

</%def>

<%def name="content()">
<form method="POST" id="" action="${a_url}/manage/add_meter">
  <table>
    <tr> 
      <td>
      <label>Meter name </label>
      </td>
      <td>
        <input type="text" name="meter-name" value="" />
      </td>
    </tr>
    <tr>
      <td>
      <label>Meter phone number </label>
      </td>
      <td> 
        <input type="text" name="meter-phone" value="" />
      </td>
    </tr>
    <tr> 
      <td><label>Meter location</label></td>
      <td> <input type="text" name="meter-location" value="" />
    </tr>
    <tr> 
      <td><label>Meter battery capacity</label></td>
      <td> <input type="text" name="battery-capacity" value="" /> </td>
    </tr>
    <tr>
      <td><label>Meter panel capacity </label></td>
      <td><input type="text" name="panel-capacity" value="" /></td>
    </tr>
    <td><label>Meter Communication Interface</label></td>
    <td> 
      <select name="communication-interface">
        % for comm in comms:
          <option value="${comm.id}">${comm}</option>
        % endfor
      </select>
    </td>
    <tr>
      <td>
        <hr /></td>
      <td>
        <hr /></td>
    </tr>
    <tr> 
      <td> 
        <label>Number of circuits to add</label>
      </td>
      <td><input type="text" name="number-of-circuits" value="" /></td>
    </tr>
    <tr> 
      <td><label>Default energy max for new circuits</label></td>
      <td> <input type="text" name="default-emax" value="" /></td>
    </tr>
    <tr>
      <td><label>Default power max for new circuits</label></td>
      <td><input type="text" name="default-power" value="" /></td>
    </tr>
    <tr>
      <td><label>Default language for each circuit</label></td>
      <td>
        <select name="default-language">
          <option name="en" value="en">English</option>
          <option name="fr" value="fr">French</option>
        </select>
      </td>
    </tr>
    <tr> 
      <td></td>
      <td><input type="submit" name="" 
                 value="Add new meter and associated circuits" /></td>
    </tr>
  </table>


</form>

</%def>
