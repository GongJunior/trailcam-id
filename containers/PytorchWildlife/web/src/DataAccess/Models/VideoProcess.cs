using System;
using System.Collections.Generic;

namespace Homebase.DataAccess.Models;

public partial class VideoProcess
{
    public int Id { get; set; }

    public string BatchName { get; set; } = null!;

    public string VideoName { get; set; } = null!;

    public DateTime? SubmitTime { get; set; }

    public DateTime? CompletedTime { get; set; }

    public string Status { get; set; } = null!;

    public string SourceFile { get; set; } = null!;

    public string? ProcessedFile { get; set; }

    public string FileHash { get; set; } = null!;

    public int FileSize { get; set; }

    public virtual ICollection<ClassifiedAnimal> ClassifiedAnimals { get; set; } = new List<ClassifiedAnimal>();
}
