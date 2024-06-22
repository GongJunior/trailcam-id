using System;
using System.Collections.Generic;

namespace Homebase.DataAccess.Models;

public partial class ClassNameMap
{
    public int Id { get; set; }

    public string ClassifierName { get; set; } = null!;

    public string DisplayName { get; set; } = null!;

    public string DisplayDescription { get; set; } = null!;
}
