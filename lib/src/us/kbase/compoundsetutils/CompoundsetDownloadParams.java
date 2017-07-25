
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
    "workspace_name",
    "compound_set_name",
    "output_format"
})
public class CompoundsetDownloadParams {

    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("compound_set_name")
    private String compoundSetName;
    @JsonProperty("output_format")
    private String outputFormat;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("workspace_name")
    public String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public CompoundsetDownloadParams withWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("compound_set_name")
    public String getCompoundSetName() {
        return compoundSetName;
    }

    @JsonProperty("compound_set_name")
    public void setCompoundSetName(String compoundSetName) {
        this.compoundSetName = compoundSetName;
    }

    public CompoundsetDownloadParams withCompoundSetName(String compoundSetName) {
        this.compoundSetName = compoundSetName;
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
        return ((((((((("CompoundsetDownloadParams"+" [workspaceName=")+ workspaceName)+", compoundSetName=")+ compoundSetName)+", outputFormat=")+ outputFormat)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
