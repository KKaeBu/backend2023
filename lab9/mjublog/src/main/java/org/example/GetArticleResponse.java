package org.example;

import com.fasterxml.jackson.annotation.JsonProperty;

public class GetArticleResponse {
    public String title;
    @JsonProperty("number")
    public int num;
}
