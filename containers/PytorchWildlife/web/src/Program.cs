using Homebase.Components;
using Homebase.DataAccess;
using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddRazorComponents()
    .AddInteractiveServerComponents();
builder.Services.AddQuickGridEntityFrameworkAdapter();
builder.Services.AddHttpClient("vidservice", httpClient => httpClient.BaseAddress = new Uri("http://vidapp:8000/"));
builder.Services.AddDbContextFactory<WildlifeContext>(options =>
    options.UseSqlite("Data Source=C:\\Users\\antho\\repos\\trailcam-id\\containers\\PytorchWildlife\\app\\data\\wildlife.db"));


var app = builder.Build();

// Configure the HTTP request pipeline.
if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Error", createScopeForErrors: true);
    // The default HSTS value is 30 days. You may want to change this for production scenarios, see https://aka.ms/aspnetcore-hsts.
    app.UseHsts();
}

app.UseHttpsRedirection();

app.UseStaticFiles();
app.UseAntiforgery();

app.MapRazorComponents<App>()
    .AddInteractiveServerRenderMode();

app.Run();
