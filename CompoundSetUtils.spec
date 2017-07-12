/*
A KBase module: CompoundSetUtils
Contains tools for import & export of compound sets
*/

module CompoundSetUtils {
    typedef string obj_ref;

    typedef structure {
        string report_name;
        string report_ref;
        obj_ref compoundset_ref;
    } compoundset_upload_results;

    /*
        CompoundSetFromFile
        string staging_file_path
    */

    funcdef compound_set_from_file(string staging_file_path)
        returns (compoundset_upload_results output) authentication required;

    typedef structure {
        string report_name;
        string report_ref;
    } compoundset_download_results;

    /*
        CompoundSetToFile
        obj_ref compound_set_ref
        string output_format
    */

    funcdef compound_set_to_file(obj_ref compound_set_ref, string output_format)
        returns (compoundset_download_results output) authentication required;

    /*
        CompoundSetFromModel
        obj_ref model_ref
    */

    funcdef compound_set_from_model(obj_ref model_ref)
        returns (compoundset_download_results output) authentication required;
};
