import transistordatabase as tdb
tdb.update_from_fileexchange()
tdb.print_tdb()

t1 = tdb.load('ROHMSemiconductor_SCT3120AW7')
t1.export_datasheet()
t2 = tdb.load('Infineon_IPW65R090CFD7')
t2.export_datasheet()