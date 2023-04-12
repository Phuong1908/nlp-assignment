from parser import ADtime , Bus
import pdb

raw_database = ["(BUS B1)",
                "(BUS B2)",
                "(BUS B3)",
                "(BUS B4)",
                "(ATIME B1 HUE 22:00HR)",
                "(DTIME B1 HCMC 10:00HR)",
                "(BUS B2)",
                "(ATIME B2 HUE 22:30HR)",
                "(DTIME B2 HCMC 12:30HR)",
                "(BUS B3)",
                "(ATIME B3 HCMC 05:00HR)", 
                "(DTIME B3 DANANG 19:00HR)",
                "(BUS B4)",
                "(ATIME B4 HCMC 5:30HR)" ,
                "(DTIME B4 DANANG 17:30HR)",
                "(ATIME B5 DANANG 13:30HR)", 
                "(DTIME B5 HUE 8:30HR)" ,
                "(ATIME B6 DANANG 9:30HR)",
                "(DTIME B6 HUE 5:30HR)",
                "(ATIME B7 HCMC 20:30HR)", "(DTIME B7 HUE 8:30HR)"
                ]


def categorize_database(database):
    """
    Categorize raw database to collections of FLIGHT, ATIME and DTIME
    ----------------------------------------------------------------
    Args:
        database: raw database from assignments (List of string values)
    """
    #Remove ( )
    buses = [data.replace('(', '').replace(')', '')
            for data in database if 'BUS' in data]
    arrival_times = [data.replace('(', '').replace(')', '')
            for data in database if 'ATIME' in data]
    departure_times = [data.replace('(', '').replace(')', '')
            for data in database if 'DTIME' in data]
    return {'bus': buses,
            'arrival': arrival_times,
            'departure': departure_times}


def retrieve_result(semantics):
    """
    Retrieve result list from procedure semantics
    ---------------------------------------------
    Args:
        semantics: dictionary created from nlp_parser.parse_to_procedure()
        semantics: SemanticProcedure object from parser.parser  
    """
    procedure_semantics = semantics
    database = categorize_database(raw_database)

    # remove unknown args: ?t ?f ?s
    dict_semantics = {
        "bus": "BUS",
        "a_loc": '',
        "a_time": '',
        "d_loc": '',
        "d_time": ''
    }
    queries = procedure_semantics.query_list  #get list of query
    result_type = 'bus'
    
    # remove unknown args: ?t ?f ?s
    for query in queries:
        if type(query) is ADtime:
            if query.name == "ATIME":
                dict_semantics["a_loc"] = '' if '?' in query.s_var else query.s_var
                dict_semantics["a_time"] = '' if '?' in query.t_var else query.t_var
            else:
                dict_semantics["d_loc"] = '' if '?' in query.s_var else query.s_var
                dict_semantics["d_time"] = '' if '?' in query.t_var else query.t_var
    # Iterate after BUS, ATIME and DTIME to have result
    bus_check_result = [
        f.split()[1] for f in database['bus'] if dict_semantics['bus'][0] in f]

    arrival_bus_result = [a.split()[1] for a in database['arrival']
            if dict_semantics['a_loc'] in a
                and dict_semantics['a_time'] in a
                and a.split()[1] in bus_check_result]

    departure_bus_result = [d.split()[1] for d in database['departure']
            if dict_semantics['d_loc'] in d
                and dict_semantics['d_time'] in d
                and d.split()[1] in arrival_bus_result]

    if result_type == 'bus':
        result = departure_bus_result
    elif result_type == 'arrival_time':
        result = [a.split()[3] for a in database['arrival']
                if a.split()[1] in departure_bus_result]
    else:
        result = [d.split()[3] for d in database['departure']
                if d.split()[1] in departure_bus_result]
    result_str = ' '.join(map(str, result))
    return result_str
