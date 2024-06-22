using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace Homebase.DataAccess.Migrations
{
    /// <inheritdoc />
    public partial class CreateVideoAnimalNameView : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.Sql(@"
            CREATE VIEW vw_VideoStatusAnimalConfidence AS
            select 
                v.video_name, 
                v.status, 
                m.display_name, 
                avg(c.confidence) as average_confidence 
            from video_process v 
            join classified_animal c on c.video_id = v.id 
            join class_name_map m on m.classifier_name = c.animal_name 
            group by v.video_name, v.status, m.display_name
            ");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.Sql("DROP VIEW vw_VideoStatusAnimalConfidence");
        }
    }
}
