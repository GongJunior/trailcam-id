using System;
using System.Collections.Generic;

namespace Homebase.DataAccess.Models;

public partial class IdxLog
{
    public string? VidName { get; set; }

    public int? FrameIdx { get; set; }

    public string? Prediction { get; set; }

    public double? Confidence { get; set; }
}
