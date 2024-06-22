using System;
using System.Collections.Generic;

namespace Homebase.DataAccess.Models;

public partial class ClassifiedAnimal
{
    public int Id { get; set; }

    public int VideoId { get; set; }

    public string AnimalName { get; set; } = null!;

    public double Confidence { get; set; }

    public virtual VideoProcess Video { get; set; } = null!;
}
