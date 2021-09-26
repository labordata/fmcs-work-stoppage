work_stoppages.db : work_stoppages.csv
	csvs-to-sqlite $^ $@

work_stoppages.csv : $(patsubst %.xlsx,%.csv,$(notdir $(wildcard raw/*.xlsx)))
	csvstack $^ | \
            python scripts/clean.py | \
            csvsql --query 'select * from (select * from stdin order by "Case Number", "Start Date", "End Date" desc nulls last, "Union Local" nulls last, "BU" nulls last, "NAICS" nulls last, "# Idled" nulls last, "Duration" desc nulls last) t group by "Case Number", "Start Date"' > $@

%.csv : raw/%.xlsx
	in2csv $< | \
            sed -n '/Industry/,$$p' | \
            sed '1s/Union Name/Union/' | \
            sed '1s/Employer Name/Employer/' | \
            sed '1s/FMCS Case Number/Case Number/' | \
            sed '1s/WS Begin Date/Start Date/' | \
            sed '1s/Duration  /Duration/' | \
            sed '1s/WS End Date/End Date/' | \
	    csvgrep -c 1 -m 'Ongoing Cases' -i | \
	    csvgrep -c 1 -m 'Ended Cases' -i | \
            csvcut -x > $@

