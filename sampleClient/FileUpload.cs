using System.Text.Json.Serialization;

public class FileUpload
{
    [JsonPropertyName("batch_name")]
    public required string BatchName { get; set; }

    [JsonPropertyName("video_name")]
    public required string VideoName { get; set; }

    [JsonPropertyName("id")]
    public int Id { get; set; }

    [JsonPropertyName("file_hash")]
    public required string FileHash { get; set; }

    [JsonPropertyName("status")]
    public required string Status { get; set; }

    [JsonPropertyName("source_file")]
    public required string SourceFile { get; set; }

    [JsonPropertyName("processed_file")]
    public string? ProcessedFile { get; set; }

    [JsonPropertyName("submit_time")]
    public string? SubmitTime { get; set; }

    [JsonPropertyName("completed_time")]
    public string? CompletedTime { get; set; }
}