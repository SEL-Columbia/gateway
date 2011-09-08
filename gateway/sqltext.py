""" Module maintaining SQL queries """

""" 
    calculate credit sum for a circuit using an 'offset join'
    technique to achieve 'pairwise diff'
"""
credit_sum_query = """
select coalesce(sum(diff), 0) from 
  (select (first_pairs.credit - second_pairs.credit) diff from
    (select credit, ((row_number() over ()) + 1) rownum from 
      (select base.credit, base.created_seconds - base.date_seconds seconds_diff from 
        (select pl.credit, l.date, pl.created, extract(epoch from pl.created) created_seconds, extract(epoch from l.date) date_seconds from 
          log l, 
          primary_log pl 
          where l.id=pl.id and 
		l.date > :start_date and 
		l.date <= :end_date and 
		pl.circuit_id = :circuit_id
          order by l.date) base
      where (base.created_seconds - base.date_seconds) < 3600) log_seconds
     ) first_pairs,
    (select credit, row_number() over () rownum from 
      (select base.credit, base.created_seconds - base.date_seconds seconds_diff from 
        (select pl.credit, l.date, pl.created, extract(epoch from pl.created) created_seconds, extract(epoch from l.date) date_seconds from 
          log l, 
          primary_log pl 
          where l.id=pl.id and 
		l.date > :start_date and 
		l.date <= :end_date and 
		pl.circuit_id = :circuit_id
          order by l.date) base
      where (base.created_seconds - base.date_seconds) < 3600) log_seconds
     ) second_pairs
   where first_pairs.rownum = second_pairs.rownum) credit_diff
 where diff > 0
"""

"""
  Detect meter reporting gaps based on pairwise diffs of
  gateway times (uses 'offset join' technique)
"""
gap_query = """
select * from 
  (select 
    m.name meter_name, 
    end_circuit, 
    time_diff.start_gateway_time, 
    time_diff.end_gateway_time, 
    time_diff.start_meter_time, 
    time_diff.end_meter_time, 
    time_diff.gap_seconds 
    from
    (select 
      second_pairs.meter_id, 
      second_pairs.circuit_id end_circuit,
      first_pairs.gateway_time start_gateway_time, 
      second_pairs.gateway_time end_gateway_time,
      first_pairs.meter_time start_meter_time,
      second_pairs.meter_time end_meter_time,
      (second_pairs.gateway_seconds - first_pairs.gateway_seconds) gap_seconds
      from
      (select *, extract(epoch from gateway_time) gateway_seconds, ((row_number() over ()) + 1) rownum from
        (select pl.circuit_id, c.meter meter_id, l.date meter_time, pl.created gateway_time from 
          log l, 
          primary_log pl,
          circuit c 
          where l.id=pl.id and 
                pl.circuit_id=c.id
        union
        select '-1' circuit_id, id meter_id, now() meter_time, now() gateway_time from meter
        order by meter_id, gateway_time) merged_log
      ) first_pairs,
      (select *, extract(epoch from gateway_time) gateway_seconds, (row_number() over ()) rownum from
        (select pl.circuit_id, c.meter meter_id, l.date meter_time, pl.created gateway_time from 
          log l, 
          primary_log pl,
          circuit c 
          where l.id=pl.id and 
                pl.circuit_id=c.id
        union
        select '-1' circuit_id, id meter_id, now() meter_time, now() gateway_time from meter
        order by meter_id, gateway_time) merged_log
      ) second_pairs 
      where first_pairs.rownum = second_pairs.rownum and first_pairs.meter_id=second_pairs.meter_id) time_diff,
    meter m
  where time_diff.meter_id = m.id) time_diff_view
where gap_seconds > :gap_seconds and start_gateway_time > :start_date and start_gateway_time <= :end_date
"""
