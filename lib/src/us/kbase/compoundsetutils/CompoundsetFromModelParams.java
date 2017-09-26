
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
 * <p>Original spec-file type: compoundset_from_model_params</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "workspace_id",
    "model_ref",
    "compound_set_name"
})
public class CompoundsetFromModelParams {

    @JsonProperty("workspace_id")
    private String workspaceId;
    @JsonProperty("model_ref")
    private String modelRef;
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

    public CompoundsetFromModelParams withWorkspaceId(String workspaceId) {
        this.workspaceId = workspaceId;
        return this;
    }

    @JsonProperty("model_ref")
    public String getModelRef() {
        return modelRef;
    }

    @JsonProperty("model_ref")
    public void setModelRef(String modelRef) {
        this.modelRef = modelRef;
    }

    public CompoundsetFromModelParams withModelRef(String modelRef) {
        this.modelRef = modelRef;
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

    public CompoundsetFromModelParams withCompoundSetName(String compoundSetName) {
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
        return ((((((((("CompoundsetFromModelParams"+" [workspaceId=")+ workspaceId)+", modelRef=")+ modelRef)+", compoundSetName=")+ compoundSetName)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
