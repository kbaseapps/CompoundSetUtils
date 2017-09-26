
package us.kbase.compoundsetutils;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: compoundset_download_params</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "compound_set_ref",
    "output_format"
})
public class CompoundsetDownloadParams {

    @JsonProperty("compound_set_ref")
    private String compoundSetRef;
    @JsonProperty("output_format")
    private String outputFormat;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("compound_set_ref")
    public String getCompoundSetRef() {
        return compoundSetRef;
    }

    @JsonProperty("compound_set_ref")
    public void setCompoundSetRef(String compoundSetRef) {
        this.compoundSetRef = compoundSetRef;
    }

    public CompoundsetDownloadParams withCompoundSetRef(String compoundSetRef) {
        this.compoundSetRef = compoundSetRef;
        return this;
    }

    @JsonProperty("output_format")
    public String getOutputFormat() {
        return outputFormat;
    }

    @JsonProperty("output_format")
    public void setOutputFormat(String outputFormat) {
        this.outputFormat = outputFormat;
    }

    public CompoundsetDownloadParams withOutputFormat(String outputFormat) {
        this.outputFormat = outputFormat;
        return this;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return ((((((("CompoundsetDownloadParams"+" [compoundSetRef=")+ compoundSetRef)+", outputFormat=")+ outputFormat)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
