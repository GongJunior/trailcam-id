// See https://aka.ms/new-console-template for more information
using System.Net;
using System.Net.Http.Headers;
using System.Net.Http.Json;
using System.Text;

Console.WriteLine("Running tests for animal identification REST api");

var vids = new DirectoryInfo(".").Parent!
    .GetDirectories()
    .Where(d => d.Name == "videos")
    .FirstOrDefault()!
    .GetFiles()
    .Where(f => f.Extension.ToLower() == ".avi");

var client = new HttpClient
{
    BaseAddress = new Uri("http://localhost:8000"),
    DefaultRequestHeaders =
    {
        Accept = { new MediaTypeWithQualityHeaderValue("application/json") }
    }
};

Console.WriteLine("Sending request to /");
var response = await client.GetAsync("/");
response.EnsureSuccessStatusCode();
Console.WriteLine($"Response: {await response.Content.ReadAsStringAsync()}");

Console.WriteLine("Sending POST request to /videoupload");
var uploads = await Task.WhenAll(vids.Select(UploadFile));
var vidsProcessing = true;
var vidsToProcess = uploads.Where(u => u is not null).Count();
var vidsCompleted = 0;
while (vidsProcessing)
{
    foreach (var upload in uploads)
    {
        if (upload != null)
        {
            Console.WriteLine($"Uploaded {upload.VideoName} with id {upload.Id}");
            Console.WriteLine($"Sending GET request to /videoupload/{upload.Id}");
            var item = await CheckStatus(upload.Id);
            if (item?.Status == "completed")
            {
                Console.WriteLine($"Video {item.VideoName} has been processed");
                vidsCompleted++;
            }
            else
            {
                Console.WriteLine($"Video {item.VideoName} is still processing");
            }
        }
    }
    if (vidsCompleted >= vidsToProcess)
    {
        vidsProcessing = false;
    }
    await Task.Delay(5000);
}





async Task<FileUpload?> CheckStatus(int id)
{
    var response = await client.GetAsync($"/videoupload/{id}");
    if (response.StatusCode == HttpStatusCode.InternalServerError ||
        response.StatusCode == HttpStatusCode.NotFound)
    {
        Console.WriteLine($"Error with request for {id}");
        Console.WriteLine(await response.Content.ReadAsStringAsync());
    };
    response.EnsureSuccessStatusCode();
    return await response.Content.ReadFromJsonAsync<FileUpload>();
}
async Task<FileUpload?> UploadFile(FileInfo file)
{
    try
    {
        using var filestream = file.OpenRead();
        var content = new MultipartFormDataContent
        {
            { new StreamContent(filestream), "file", file.Name },
            { new StringContent("test1", Encoding.UTF8), "batch_name" }
        };
        var response = await client.PostAsync("/videoupload", content);
        if (response.StatusCode == HttpStatusCode.UnprocessableEntity ||
            response.StatusCode == HttpStatusCode.InternalServerError ||
            response.StatusCode == HttpStatusCode.BadRequest)
        {
            Console.WriteLine($"Error with request for {file.Name}");
            Console.WriteLine(await response.Content.ReadAsStringAsync());
            return null;
        }
        response.EnsureSuccessStatusCode();
        return await response.Content.ReadFromJsonAsync<FileUpload>();
    }
    catch (Exception ex)
    {
        Console.WriteLine($"Failed to upload {file.Name}");
        Console.WriteLine(ex.Message);
        return null;
    }
}