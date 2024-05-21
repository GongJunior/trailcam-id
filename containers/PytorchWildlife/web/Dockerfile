FROM mcr.microsoft.com/dotnet/sdk:8.0 as build-env
WORKDIR /app
COPY ./src ./
RUN dotnet restore Homebase.csproj
RUN dotnet publish Homebase.csproj -c Release -o out

FROM mcr.microsoft.com/dotnet/aspnet:8.0
WORKDIR /app
COPY --from=build-env /app/out .
ENTRYPOINT [ "dotnet", "Homebase.dll" ]