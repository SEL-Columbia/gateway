
select a.token, 
       a.value as token_value, 
       a.created as vendor_purchase, 
       c.pin as circuit_account,
       c.meter, 
       a.end as vendor_upload
  from circuit as c join
    (select a.id, 
          a.credit,
          a.end,
          a.start, 
          a.token_id, 
          a.circuit_id, 
          token.token, 
          token.value, 
          token.created from token join
    (select jobs.id, 
            addcredit.credit, 
            addcredit.token_id, 
            jobs.circuit_id, jobs.start, jobs.end
        from addcredit left outer join jobs 
        on (addcredit.id = jobs.id)) a on (token.id = a.token_id))
            a on (c.id = a.circuit_id) order by c.meter;
