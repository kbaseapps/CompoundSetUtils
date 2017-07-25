
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
    "workspace_name",
    "model_name",
    "compound_set_name"
})
public class CompoundsetFromModelParams {

    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("model_name")
    private String modelName;
    @JsonProperty("compound_set_name")
    private String compoundSetName;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("workspace_name")
    public String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public CompoundsetFromModelParams withWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("model_name")
    public String getModelName() {
        return modelName;
    }

    @JsonProperty("model_name")
    public void setModelName(String modelName) {
        this.modelName = modelName;
    }

    public CompoundsetFromModelParams withModelName(String modelName) {
        this.modelName = modelName;
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
        return ((((((((("CompoundsetFromModelParams"+" [workspaceName=")+ workspaceName)+", modelName=")+ modelName)+", compoundSetName=")+ compoundSetName)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
