using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace Homebase.DataAccess.Migrations
{
    /// <inheritdoc />
    public partial class InitialCreate : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "class_name_map",
                columns: table => new
                {
                    id = table.Column<int>(type: "INTEGER", nullable: false),
                    classifier_name = table.Column<string>(type: "VARCHAR", nullable: false),
                    display_name = table.Column<string>(type: "VARCHAR", nullable: false),
                    display_description = table.Column<string>(type: "VARCHAR", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_class_name_map", x => x.id);
                });

            migrationBuilder.CreateTable(
                name: "idx_logs",
                columns: table => new
                {
                    vid_name = table.Column<string>(type: "TEXT", nullable: true),
                    frame_idx = table.Column<int>(type: "INT", nullable: true),
                    prediction = table.Column<string>(type: "TEXT", nullable: true),
                    confidence = table.Column<double>(type: "REAL", nullable: true)
                },
                constraints: table =>
                {
                });

            migrationBuilder.CreateTable(
                name: "video_process",
                columns: table => new
                {
                    id = table.Column<int>(type: "INTEGER", nullable: false),
                    batch_name = table.Column<string>(type: "VARCHAR", nullable: false),
                    video_name = table.Column<string>(type: "VARCHAR", nullable: false),
                    submit_time = table.Column<DateTime>(type: "DATETIME", nullable: true, defaultValueSql: "CURRENT_TIMESTAMP"),
                    completed_time = table.Column<DateTime>(type: "DATETIME", nullable: true),
                    status = table.Column<string>(type: "VARCHAR", nullable: false),
                    source_file = table.Column<string>(type: "VARCHAR", nullable: false),
                    processed_file = table.Column<string>(type: "VARCHAR", nullable: true),
                    file_hash = table.Column<string>(type: "VARCHAR", nullable: false),
                    file_size = table.Column<int>(type: "INTEGER", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_video_process", x => x.id);
                });

            migrationBuilder.CreateTable(
                name: "classified_animal",
                columns: table => new
                {
                    id = table.Column<int>(type: "INTEGER", nullable: false),
                    video_id = table.Column<int>(type: "INTEGER", nullable: false),
                    animal_name = table.Column<string>(type: "VARCHAR", nullable: false),
                    confidence = table.Column<double>(type: "FLOAT", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_classified_animal", x => x.id);
                    table.ForeignKey(
                        name: "FK_classified_animal_video_process_video_id",
                        column: x => x.video_id,
                        principalTable: "video_process",
                        principalColumn: "id");
                });

            migrationBuilder.CreateIndex(
                name: "ix_class_name_map_id",
                table: "class_name_map",
                column: "id");

            migrationBuilder.CreateIndex(
                name: "ix_classified_animal_id",
                table: "classified_animal",
                column: "id");

            migrationBuilder.CreateIndex(
                name: "IX_classified_animal_video_id",
                table: "classified_animal",
                column: "video_id");

            migrationBuilder.CreateIndex(
                name: "ix_video_process_id",
                table: "video_process",
                column: "id");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "class_name_map");

            migrationBuilder.DropTable(
                name: "classified_animal");

            migrationBuilder.DropTable(
                name: "idx_logs");

            migrationBuilder.DropTable(
                name: "video_process");
        }
    }
}
