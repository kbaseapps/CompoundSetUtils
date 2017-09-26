
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
 * <p>Original spec-file type: compoundset_upload_params</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "workspace_id",
    "staging_file_path",
    "compound_set_name"
})
public class CompoundsetUploadParams {

    @JsonProperty("workspace_id")
    private String workspaceId;
    @JsonProperty("staging_file_path")
    private String stagingFilePath;
    @JsonProperty("compound_set_name")
    private String compoundSetName;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("workspace_id")
    public String getWorkspaceId() {
        return workspaceId;
    }

    @JsonProperty("workspace_id")
    public void setWorkspaceId(String workspaceId) {
        this.workspaceId = workspaceId;
    }

    public CompoundsetUploadParams withWorkspaceId(String workspaceId) {
        this.workspaceId = workspaceId;
        return this;
    }

    @JsonProperty("staging_file_path")
    public String getStagingFilePath() {
        return stagingFilePath;
    }

    @JsonProperty("staging_file_path")
    public void setStagingFilePath(String stagingFilePath) {
        this.stagingFilePath = stagingFilePath;
    }

    public CompoundsetUploadParams withStagingFilePath(String stagingFilePath) {
        this.stagingFilePath = stagingFilePath;
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

    public CompoundsetUploadParams withCompoundSetName(String compoundSetName) {
        this.compoundSetName = compoundSetName;
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
        return ((((((((("CompoundsetUploadParams"+" [workspaceId=")+ workspaceId)+", stagingFilePath=")+ stagingFilePath)+", compoundSetName=")+ compoundSetName)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
