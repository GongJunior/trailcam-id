using System;
using System.Collections.Generic;
using Homebase.DataAccess.Models;
using Microsoft.EntityFrameworkCore;

namespace Homebase.DataAccess;

public partial class WildlifeContext : DbContext
{
    public WildlifeContext()
    {
    }

    public WildlifeContext(DbContextOptions<WildlifeContext> options)
        : base(options)
    {
    }

    public virtual DbSet<ClassNameMap> ClassNameMaps { get; set; }

    public virtual DbSet<ClassifiedAnimal> ClassifiedAnimals { get; set; }

    public virtual DbSet<IdxLog> IdxLogs { get; set; }

    public virtual DbSet<VideoProcess> VideoProcesses { get; set; }
    public virtual DbSet<VideoStatusAnimalConfidence> VideoStatusAnimalConfidences { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<ClassNameMap>(entity =>
        {
            entity.ToTable("class_name_map");

            entity.HasIndex(e => e.Id, "ix_class_name_map_id");

            entity.Property(e => e.Id)
                .ValueGeneratedNever()
                .HasColumnName("id");
            entity.Property(e => e.ClassifierName)
                .HasColumnType("VARCHAR")
                .HasColumnName("classifier_name");
            entity.Property(e => e.DisplayDescription)
                .HasColumnType("VARCHAR")
                .HasColumnName("display_description");
            entity.Property(e => e.DisplayName)
                .HasColumnType("VARCHAR")
                .HasColumnName("display_name");
        });

        modelBuilder.Entity<ClassifiedAnimal>(entity =>
        {
            entity.ToTable("classified_animal");

            entity.HasIndex(e => e.Id, "ix_classified_animal_id");

            entity.Property(e => e.Id)
                .ValueGeneratedNever()
                .HasColumnName("id");
            entity.Property(e => e.AnimalName)
                .HasColumnType("VARCHAR")
                .HasColumnName("animal_name");
            entity.Property(e => e.Confidence)
                .HasColumnType("FLOAT")
                .HasColumnName("confidence");
            entity.Property(e => e.VideoId).HasColumnName("video_id");

            entity.HasOne(d => d.Video).WithMany(p => p.ClassifiedAnimals)
                .HasForeignKey(d => d.VideoId)
                .OnDelete(DeleteBehavior.ClientSetNull);
        });

        modelBuilder.Entity<IdxLog>(entity =>
        {
            entity
                .HasNoKey()
                .ToTable("idx_logs");

            entity.Property(e => e.Confidence).HasColumnName("confidence");
            entity.Property(e => e.FrameIdx)
                .HasColumnType("INT")
                .HasColumnName("frame_idx");
            entity.Property(e => e.Prediction).HasColumnName("prediction");
            entity.Property(e => e.VidName).HasColumnName("vid_name");
        });

        modelBuilder.Entity<VideoProcess>(entity =>
        {
            entity.ToTable("video_process");

            entity.HasIndex(e => e.Id, "ix_video_process_id");

            entity.Property(e => e.Id)
                .ValueGeneratedNever()
                .HasColumnName("id");
            entity.Property(e => e.BatchName)
                .HasColumnType("VARCHAR")
                .HasColumnName("batch_name");
            entity.Property(e => e.CompletedTime)
                .HasColumnType("DATETIME")
                .HasColumnName("completed_time");
            entity.Property(e => e.FileHash)
                .HasColumnType("VARCHAR")
                .HasColumnName("file_hash");
            entity.Property(e => e.FileSize).HasColumnName("file_size");
            entity.Property(e => e.ProcessedFile)
                .HasColumnType("VARCHAR")
                .HasColumnName("processed_file");
            entity.Property(e => e.SourceFile)
                .HasColumnType("VARCHAR")
                .HasColumnName("source_file");
            entity.Property(e => e.Status)
                .HasColumnType("VARCHAR")
                .HasColumnName("status");
            entity.Property(e => e.SubmitTime)
                .HasDefaultValueSql("CURRENT_TIMESTAMP")
                .HasColumnType("DATETIME")
                .HasColumnName("submit_time");
            entity.Property(e => e.VideoName)
                .HasColumnType("VARCHAR")
                .HasColumnName("video_name");
        });

        modelBuilder.Entity<VideoStatusAnimalConfidence>(entity =>
        {
            entity.HasNoKey();

            entity.ToView("vw_VideoStatusAnimalConfidence");

            entity.Property(e => e.AverageConfidence)
                .HasColumnType("FLOAT")
                .HasColumnName("average_confidence");
            entity.Property(e => e.AnimalName)
                .HasColumnType("VARCHAR")
                .HasColumnName("display_name");
            entity.Property(e => e.Status)
                .HasColumnType("VARCHAR")
                .HasColumnName("status");
            entity.Property(e => e.VideoName)
                .HasColumnType("VARCHAR")
                .HasColumnName("video_name");
        });

        OnModelCreatingPartial(modelBuilder);
    }

    partial void OnModelCreatingPartial(ModelBuilder modelBuilder);
}
